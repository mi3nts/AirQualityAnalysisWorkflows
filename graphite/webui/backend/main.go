// A simple RESTful backend server that launches ingestion on receipt.
//
// Based on Fiber, at https://github.com/gofiber/fiber.
//
// Can be queried for status of ingestion as well as remove ingested data from
// the Graphite container.

package main

import (
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"time"

	"github.com/gofiber/fiber/v2"
)

type statusType int

const (
	STATUS_IDLE statusType = iota
	STATUS_INGESTING
	STATUS_DELETING
)

var statusMap = map[statusType]string{STATUS_IDLE: "idle", STATUS_INGESTING: "ingesting", STATUS_DELETING: "deleting"}

func main() {
	// Check for Graphite up
	for _, err := http.Get("graphite:8008"); err != nil; {
		log.Printf("Graphite deletion handler not up; retrying")
		time.Sleep(2 * time.Second)
	}

	currentStatus := STATUS_IDLE
	actionNotify := make(chan statusType)
	defer close(actionNotify)
	go func(ingestNotify <-chan statusType) {
		for {
			action := <-actionNotify
			switch action {
			case STATUS_INGESTING:
				// Start ingestion
				currentStatus = STATUS_INGESTING
				ingestCmd := exec.Command("node", "/scripts/start.mjs")
				if err := ingestCmd.Run(); err != nil {
					log.Fatal(err)
				}

				// Finish ingestion
				currentStatus = STATUS_IDLE
			case STATUS_DELETING:
				// Start deleting
				currentStatus = STATUS_DELETING
				if resp, err := http.Get("graphite:8008/delete"); err != nil || resp.StatusCode != 200 {
					log.Fatal(err)
				}
				time.Sleep(10 * time.Second) // TODO: figure out a better way to tell if server deleted whisper data

				// Finish ingestion
				currentStatus = STATUS_IDLE
			case STATUS_IDLE: // taken as finish program
				return
			}

		}
	}(actionNotify)

	app := fiber.New()

	// Default handler
	app.Get("/", func(c *fiber.Ctx) error {
		// Requires an action
		return c.SendStatus(404)
	})

	// Status report handler
	app.Get("/status", func(c *fiber.Ctx) error {
		return c.SendString(statusMap[currentStatus])
	})

	// Start ingestion handler
	app.Get("/ingest", func(c *fiber.Ctx) error {
		if currentStatus != STATUS_IDLE {
			return c.Status(409).SendString(fmt.Sprintf("Not idle; currently %s", statusMap[currentStatus]))
		}
		actionNotify <- STATUS_INGESTING

		c.WriteString("OK")
		return c.SendStatus(200)
	})

	// Start deletion handler
	app.Get("/delete", func(c *fiber.Ctx) error {
		if currentStatus != STATUS_IDLE {
			return c.Status(409).SendString(fmt.Sprintf("Not idle; currently %s", statusMap[currentStatus]))
		}
		actionNotify <- STATUS_DELETING

		c.WriteString("OK")
		return c.SendStatus(200)
	})

	app.Listen(":3000")
}

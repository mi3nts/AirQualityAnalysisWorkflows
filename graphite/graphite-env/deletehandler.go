package main

import (
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(404)
		io.WriteString(w, "not found")
	})

	http.HandleFunc("/delete", func(w http.ResponseWriter, r *http.Request) {
		if err := os.RemoveAll("/opt/graphite/storage/whisper/data"); err != nil {
			log.Printf("cannot remove data directory")
		}
		w.WriteHeader(200)
		io.WriteString(w, "deletion started")
	})

	log.Print("deletehandler running, serving on port 8008")
	log.Fatal(http.ListenAndServe(":8008", nil))
}

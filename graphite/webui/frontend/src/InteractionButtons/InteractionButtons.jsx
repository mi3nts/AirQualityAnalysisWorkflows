import { useState } from 'react'
import { Button } from '@chakra-ui/button'
import AppText from '../AppText/AppText'
import { Flex } from '@chakra-ui/layout'

function InteractionButtons() {
    const [ingestDebounce, setIngestDebounce] = useState(false)
    const [deleteDebounce, setDeleteDebounce] = useState(false)
    const [backendStatus, setBackendStatus] = useState('Check backend status.')
    const [ingestStatus, setIngestStatus] = useState('No ingestion request sent.')
    const [deleteStatus, setDeleteStatus] = useState('No deletion request sent.')

    async function getStatus() {
        const respText = await fetch(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}/status`).then(resp => resp.text())
        setBackendStatus(`Backend status: ${respText}`)
    }

    async function getIngest() {
        if (!ingestDebounce) {
            setIngestDebounce(true)
            // Check status
            if (await fetch(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}/status`).then(resp => resp.text()) !== 'idle') {
                setIngestDebounce(false)
                setIngestStatus('Backend busy')
            }

            const respText = await fetch(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}/ingest`).then(resp => resp.text()).catch(console.log)
            setTimeout(() => setIngestDebounce(false), 2000)
            if (respText === "OK") {
                setIngestStatus('Ingestion request sent successfully.')
            } else {
                setIngestStatus('Ingestion request failed.')
            }
        }
    }

    async function getDelete() {
        if (!deleteDebounce) {
            setDeleteDebounce(true)
            // Check status
            if (await fetch(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}/status`).then(resp => resp.text()) !== 'idle') {
                setIngestDebounce(false)
                setIngestStatus('Backend busy')
            }

            const respText = await fetch(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}/delete`).then(resp => resp.text()).catch(console.log)
            setTimeout(() => setDeleteDebounce(false), 2000)
            if (respText === "OK") {
                setDeleteStatus('Deletion request sent successfully.')
            } else {
                setDeleteStatus('Deletion request failed.')
            }
        }
    }

    return (
        <Flex flexDir="column" alignItems="center" mt="2rem">
            <Button onClick={getStatus}>
                Status
            </Button>
            <AppText mt="1rem">
                {backendStatus}
            </AppText>
            <Button onClick={getIngest} mt="2rem">
                Ingest
            </Button>
            <AppText mt="1rem">
                {ingestStatus}
            </AppText>
            <Button onClick={getDelete} mt="2rem">
                Delete
            </Button>
            <AppText mt="1rem">
                {deleteStatus}
            </AppText>
        </Flex>
    )
}

export default InteractionButtons
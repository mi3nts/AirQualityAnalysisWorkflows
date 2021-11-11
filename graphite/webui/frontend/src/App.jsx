import { useState, useEffect } from 'react'
import { Flex, Link } from '@chakra-ui/react'
import AppText from './AppText/AppText'
import InteractionButtons from './InteractionButtons/InteractionButtons'
import Title from './Title/Title'

function App() {
  const [access, setAccess] = useState(false)

  useEffect(() => {
    (async function() {
      const respText = await fetch(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}`).then(r => r.text()).catch(e => console.log(e))
      if (respText === 'OK') {
        setAccess(true)
      }
    })()
  }, [])

  return (
    <Flex w="100vw" p="4rem" bgColor="black" minH="100vh" m="0"
      flexDir="column" alignItems="center">
      {access ?
        <>
          <Title />
          <AppText mt="2rem">
            Grafana can be accessible <Link href={`http://localhost:${import.meta.env.VITE_GRAFANA_PORT}`}><em>here</em></Link>.
          </AppText>
          <InteractionButtons />
        </> :
        <AppText>
          Backend server not up.
        </AppText>}
    </Flex>
  )
}

export default App

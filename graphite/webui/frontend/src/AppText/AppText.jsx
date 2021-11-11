import { Text } from '@chakra-ui/react'

function AppText({ children, ...props }) {
    return (
        <Text fontFamily="Overpass; sans-serif" {...props}>
            {children}
        </Text>
    )
}

export default AppText
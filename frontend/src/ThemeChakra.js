// 1. Import the extendTheme function
import {
    extendTheme,
    withDefaultColorScheme,
    withDefaultSize,
    withDefaultVariant,
    theme as baseTheme,
} from '@chakra-ui/react'



export const themeChakra = extendTheme(
    withDefaultColorScheme({colorScheme: 'linkedin'}),
    withDefaultSize({size: 'sm'}),
    // withDefaultVariant({variant: 'outline'}),  // alert will be unfilled
    {
        fonts: {
            body: "system-ui, sans-serif",
            heading: "'PT Sans', Georgia, serif",
            mono: "Menlo, monospace",
        },
    }
)
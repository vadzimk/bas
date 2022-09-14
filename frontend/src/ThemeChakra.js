// 1. Import the extendTheme function
import {
    extendTheme,
    withDefaultColorScheme,
    withDefaultSize,
    withDefaultVariant,
    withDefaultProps,
    theme as baseTheme,
} from '@chakra-ui/react'


export const themeChakra = extendTheme(
    withDefaultColorScheme({colorScheme: 'linkedin'}),
    withDefaultSize({size: 'sm'}),
    withDefaultProps({
        defaultProps: {
            // variant: 'outline',
            size: 'sm',
            borderRadius: 'base',

        },
        // components: ['Input', 'NumberInput', 'PinInput'],
    }),

    {
        fonts: {
            body: "system-ui, sans-serif",
            heading: "'PT Sans', Georgia, serif",
            mono: "Menlo, monospace",
        },
    }
)
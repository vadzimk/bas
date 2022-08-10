import {createTheme} from '@mui/material'

const defaultTheme = createTheme()

const theme = createTheme({
    palette: {
        common: {
            orange: '#ffba60',
            danger: '#ff1744',
            green: '#00e676',
            blue: '#2196f3'
        },
    },
    typography: {
        fontFamily: 'BlinkMacSystemFont,-apple-system,"Segoe UI",Roboto,Oxygen,Ubuntu,Cantarell,"Fira Sans","Droid Sans","Helvetica Neue",Helvetica,Arial,sans-serif;',
        h1: {
            ...defaultTheme.typography.h1,
            fontFamily: "'PT Sans', sans-serif",
        },
        h2: {
            ...defaultTheme.typography.h2,
            fontFamily: "'PT Sans', sans-serif",
        },
        h3: {
            ...defaultTheme.typography.h3,
            fontFamily: "'PT Sans', sans-serif",
        }
    }
})

export default theme
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
    }
})

export default theme
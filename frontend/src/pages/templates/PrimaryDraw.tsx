import { Box, Drawer, useMediaQuery } from "@mui/material"
import { useEffect, useState } from "react"
import { useTheme } from "@mui/material/styles"


const PrimaryDraw = () => {
    const theme = useTheme()
    const below600 = useMediaQuery("(max-width:599px)")
    const [open, setOpen] = useState(!below600)

    useEffect(() => {
        setOpen(!below600)
    }, [below600])
    
    return(
        <Drawer open={open} variant="permanent">
            <Box>
                temp
            </Box>
        </Drawer>
    )
}

export default PrimaryDraw


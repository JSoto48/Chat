import { AppBar, Box, Drawer, IconButton, Link, Toolbar, Typography, useMediaQuery } from "@mui/material"
import { useTheme } from "@mui/material/styles"
import MenuIcon from "@mui/icons-material/Menu"
import { useEffect, useState } from "react"


const PrimaryAppBar = () => {
    const [sideMenu, setSideMenu] = useState(false)
    const theme = useTheme()
    const isSmallScreen = useMediaQuery(theme.breakpoints.up("sm"))

    useEffect(() => {
        if(isSmallScreen && sideMenu) {
            setSideMenu(false)
        }
    }, [isSmallScreen])     // will fire off useEffect when isSmallScreen changes

    const toggleDrawer =
    (open: boolean) => (event: React.MouseEvent | React.KeyboardEvent) => {
        if(event.type === "keydown" && ((event as React.KeyboardEvent).key === "Tab" ||
        (event as React.KeyboardEvent).key === "Shift")) {
            return
        }
        setSideMenu(open)
    }

    return (
        <AppBar
            sx={{
                zIndex: (theme) => theme.zIndex.drawer + 2,
                backgroundColor: theme.palette.background.default,
                borderBottom: `1px solid ${theme.palette.divider}`,
            }}
        >
            <Toolbar
                variant="dense"
                sx={{
                    height: theme.primaryAppBar.height,
                    minHeight: theme.primaryAppBar.height,
                }}
            >
                {/* Collapse when display is xs */}
                <Box sx={{ display: {xs: "block", sm:"none"} }}>
                    <IconButton color="inherit" aria-label="open drawer" edge="start" onClick={toggleDrawer(true)} sx={{mr:1}}>
                        <MenuIcon />
                    </IconButton>
                </Box>

                {/* open={sideMenu}, onClose={toggleDrawer(false)} */}
                <Drawer anchor="left" open={sideMenu} onClose={toggleDrawer(false)}>
                    <Typography>
                        hi
                    </Typography>
                </Drawer>

                {/* Icon */}
                <Link href="/" underline="none" color="inherit">
                    <Typography variant="h6" noWrap component="div" sx={{
                        display:{fontWeight: 700, letterSpacing: "-0.5px"}}}>
                            CHAT
                    </Typography>
                </Link>
            </Toolbar>
        </AppBar>
    )
}

export default PrimaryAppBar


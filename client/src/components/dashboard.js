import React, { useState } from 'react'
import { useNavigate } from "react-router-dom"
import { Grid, Paper, Typography, Drawer, List, ListItem, ListItemText, AppBar, Toolbar, IconButton } from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'

const Dashboard = () => {
    const [openDrawer, setOpenDrawer] = useState(false)
    const navigate = useNavigate()

    const handleDrawerOpen = () => {
        setOpenDrawer(true)
    }

    const handleDrawerClose = () => {
        setOpenDrawer(false)
    }

    const handleLogout = () => {
        localStorage.removeItem('token')
        window.location.reload(true)
    }

    const handleProfile = () => {
        navigate('/profile')
    }

    return (
        <Grid container spacing={3}>
            {/* Navbar */}
            <Grid item xs={12}>
                <AppBar position="static">
                    <Toolbar>
                        <IconButton
                            edge="start"
                            color="inherit"
                            onClick={handleDrawerOpen}
                            sx={{ marginRight: 2 }}
                        >
                            <MenuIcon />
                        </IconButton>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            Dashboard
                        </Typography>
                    </Toolbar>
                </AppBar>
            </Grid>

            {/* Sidebar */}
            <Grid item xs={2}>
                <Drawer
                    anchor="left"
                    open={openDrawer}
                    onClose={handleDrawerClose}
                    style={{ width: '10%' }}
                >
                    <List>
                        <ListItem button disabled>
                            <ListItemText primary="Dashboard" />
                        </ListItem>
                        <ListItem button onClick={handleProfile}>
                            <ListItemText primary="Profile" />
                        </ListItem>
                        <ListItem button onClick={handleLogout}>
                            <ListItemText primary="Sign Out" />
                        </ListItem>
                    </List>
                </Drawer>
            </Grid>

            {/* Main Content */}
            <Grid item xs={8}>
                {/* Dashboard Header */}
                <Paper elevation={3} style={{ padding: '20px', textAlign: 'center' }}>
                    <Typography variant="h4">Dashboard Title</Typography>
                </Paper>

                {/* Data Table */}
                <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
                    {/* Replace this with your actual dashboard content */}
                    <Typography variant="h6">Data Table</Typography>
                    {/* Your data table component goes here */}
                </Paper>

                {/* Other Dashboard Components */}
                <Grid container spacing={3} style={{ marginTop: '20px' }}>
                    <Grid item xs={6}>
                        <Paper elevation={3} style={{ padding: '20px' }}>
                            {/* Replace this with other components on your dashboard */}
                            <Typography variant="h6">Component 1</Typography>
                            {/* Your component content goes here */}
                        </Paper>
                    </Grid>

                    <Grid item xs={6}>
                        <Paper elevation={3} style={{ padding: '20px' }}>
                            {/* Replace this with other components on your dashboard */}
                            <Typography variant="h6">Component 2</Typography>
                            {/* Your component content goes here */}
                        </Paper>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}

export default Dashboard
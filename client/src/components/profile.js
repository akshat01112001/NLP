import React, { useState, useEffect } from 'react'
import { useNavigate } from "react-router-dom"
import { TextField, Paper, Container, Typography, Button, Drawer, List, ListItem, ListItemText, AppBar, Toolbar, IconButton } from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import File from './file'

const Profile = () => {
    const [token, setToken] = useState("")
    const [username, setUsername] = useState("")
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [number, setNumber] = useState("")
    const [isSidebarOpen, setSidebarOpen] = useState(false)
    const navigate = useNavigate()

    const handleSidebarToggle = () => {
        setSidebarOpen(!isSidebarOpen)
    }

    const handleDashboard = () => {
        navigate('/signin')
    }

    const handleSignOut = () => {
        localStorage.removeItem('token')
        setToken('')
        navigate('/signin')
    }

    const handleSubmit = async (event) => {
        event.preventDefault()
        
        try {
            const response = await fetch('http://localhost:8000/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, email, number, username, }),
            })

            if (response.ok) {
                const json = await response.json()
                alert(json.message)
            }
        } catch (error) {
            alert(error.message)
        }
    }

    useEffect(() => {
        const handleUsername = async () => {
            try {
                const response = await fetch('http://localhost:8000/get_user', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                })

                if (response.ok) {
                    const json = await response.json()
                    setUsername(json.sub)
                }
            } catch (error) {
                alert(error.message)
            }
        }
        const storedToken = localStorage.getItem('token')
        if (storedToken) {
            setToken(storedToken)
            handleUsername()
        }
    }, [token])

    return (
        <div>
            {/* Navbar */}
            <AppBar position="static">
                <Toolbar>
                    <Toolbar>
                        <IconButton
                            edge="start"
                            color="inherit"
                            onClick={handleSidebarToggle}
                            sx={{ marginRight: 2 }}
                        >
                            <MenuIcon />
                        </IconButton>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            Profile
                        </Typography>
                    </Toolbar>
                </Toolbar>
            </AppBar>

            {/* Sidebar */}
            <Drawer anchor="left" open={isSidebarOpen} onClose={handleSidebarToggle}>
                <List>
                    <ListItem button onClick={handleDashboard}>
                        <ListItemText primary="Dashboard" />
                    </ListItem>
                    <ListItem button disabled>
                        <ListItemText primary="Profile" />
                    </ListItem>
                    <ListItem button onClick={handleSignOut}>
                        <ListItemText primary="Sign Out" />
                    </ListItem>
                </List>
            </Drawer>

            {/* Profile Form */}
            {token && (
                <div>
                    <Container maxWidth="xs">
                        <Paper elevation={3} style={{ padding: '20px', marginTop: '50px' }}>
                            <File setName={setName} setEmail={setEmail} setNumber={setNumber} />
                        </Paper>
                    </Container>
                    <form onSubmit={handleSubmit}>
                        <Container maxWidth="xs">
                            {name && (
                                <Paper elevation={3} style={{ padding: '20px', marginTop: '50px' }}>
                                    <TextField
                                        label="Name"
                                        name="name"
                                        variant="outlined"
                                        margin="normal"
                                        fullWidth
                                        required
                                        value={name}
                                        onChange={(e) => {
                                            setName(e.target.value)
                                        }}
                                    />
                                    <TextField
                                        label="Email"
                                        type="email"
                                        name="email"
                                        variant="outlined"
                                        margin="normal"
                                        fullWidth
                                        required
                                        value={email}
                                        onChange={(e) => {
                                            setEmail(e.target.value)
                                        }}
                                    />
                                    <TextField
                                        label="Phone Number"
                                        name="number"
                                        variant="outlined"
                                        margin="normal"
                                        fullWidth
                                        required
                                        value={number}
                                        onChange={(e) => {
                                            setNumber(e.target.value)
                                        }}
                                    />
                                    <Button type="submit" variant="contained" color="primary" fullWidth>
                                        Submit
                                    </Button>
                                </Paper>
                            )}
                        </Container>
                    </form>
                </div>
            )}
        </div>
    )
}

export default Profile
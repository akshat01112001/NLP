import React, { useState } from 'react'
import { Container, Paper, TextField, Button, Typography, Link } from '@mui/material'
import { useNavigate } from "react-router-dom"

const Signup = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

    const handleSignup = async () => {
        try {
            const response = await fetch('http://localhost:8000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            })

            if (response.ok) {
                const data = await response.json()
                alert(data.message)
                navigate('/signin')
            }
        } catch (error) {
            console.error('Signup failed:', error.message)
        }
    }

    return (
        <Container maxWidth="xs">
            <Paper elevation={3} style={{ padding: '20px', marginTop: '50px' }}>
                <Typography variant="h5" align="center" gutterBottom>
                    Sign Up
                </Typography>
                <TextField
                    label="Username"
                    fullWidth
                    margin="normal"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                    label="Password"
                    fullWidth
                    margin="normal"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Button variant="outlined" color="primary" fullWidth onClick={handleSignup} style={{ marginTop: '10px', marginBottom: '10px' }}>
                    Sign Up
                </Button>
                <Typography variant="h7" align="center" gutterBottom>
                    Already have an account? <Link href="/signin">Sign In</Link>
                </Typography>
            </Paper>
        </Container>
    )
}

export default Signup
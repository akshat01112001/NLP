import React, { useState, useEffect } from 'react'
import { TextField, Button, Stack } from '@mui/material'
import File from './file'

const Profile = () => {
    const [token, setToken] = useState("")
    const [username, setUsername] = useState("")
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [number, setNumber] = useState("")

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
        token && (
            <form onSubmit={handleSubmit}>
                <File setName={setName} setEmail={setEmail} setNumber={setNumber} />
                <Stack spacing={10}>
                    {name && (
                        <div>
                            <TextField
                                label="Name"
                                name="name"
                                variant="outlined"
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
                                fullWidth
                                required
                                value={number}
                                onChange={(e) => {
                                    setNumber(e.target.value)
                                }}
                            />
                            <Button type="submit" variant="contained" color="primary">
                                Submit
                            </Button>
                        </div>
                    )}
                </Stack>
            </form>
        )
    )
}

export default Profile
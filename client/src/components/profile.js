import React, { useState, useEffect } from 'react'
import { TextField, Button, Stack } from '@mui/material'
import File from './file'

const Profile = () => {
    const [username, setUsername] = useState("")
    const [token, setToken] = useState("")
    const [data, setData] = useState()
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        number: '',
    })

    const handleChange = (field) => (event) => {
        setFormData({ ...formData, [field]: event.target.value })
    }

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

    const handleSubmit = async (event) => {
        event.preventDefault()
        await handleUsername()

        const form = new FormData()
        form.append('name', formData.name)
        form.append('email', formData.email)
        form.append('number', formData.number)
        form.append('username', username)

        try {
            const response = await fetch('http://localhost:8000/profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(form),
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
        const storedToken = localStorage.getItem('token')
        if (storedToken) {
            setToken(storedToken)
        }
    }, [data])

    return (
        token && (
            <form onSubmit={handleSubmit}>
                <File setData={setData} />
                <Stack spacing={2}>
                    {data && (
                        <div>
                            <TextField
                                label="Name"
                                name="name"
                                variant="outlined"
                                fullWidth
                                required
                                // value={formData.name}
                                defaultValue={data.name}
                                onChange={handleChange('name')}
                            />
                            <TextField
                                label="Email"
                                // type="email"
                                name="email"
                                variant="outlined"
                                fullWidth
                                required
                                // value={formData.email}
                                defaultValue={data.email[0]}
                                onChange={handleChange('email')}
                            />
                            <TextField
                                label="Phone Number"
                                name="number"
                                variant="outlined"
                                fullWidth
                                required
                                // value={formData.number}
                                defaultValue={data.number[0]}
                                onChange={handleChange('number')}
                            />
                            <Button type="submit" variant="contained" color="primary">
                                Submit
                            </Button>
                        </div>
                    )}
                </Stack>
                <Stack spacing={2}>
                    {!data && (
                        <div>
                            <TextField label="Name" variant="outlined" fullWidth disabled />
                            <TextField label="Email" type="email" variant="outlined" fullWidth disabled />
                            <TextField label="Phone Number" variant="outlined" fullWidth disabled />
                            <Button type="submit" variant="contained" color="primary" disabled>
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
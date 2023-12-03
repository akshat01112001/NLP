import React from 'react'
import { Input } from '@mui/material'

const FileUpload = ({ setData }) => {
    const handleFileChange = async (event) => {
        const file = event.target.files[0]
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData,
        })

        if (response.ok) {
            const data = await response.json()
            setData(data)
            console.log(data)
            alert('Your resume has been uploaded')
        }
    }

    return (
        <div>
            <Input
                type="file"
                inputProps={{ accept: '.doc, .docx, .pdf' }}
                onChange={handleFileChange}
                id="fileInput"
            />
        </div>
    )
}

export default FileUpload

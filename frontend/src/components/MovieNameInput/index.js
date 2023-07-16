import React from 'react';
import TextField from '@mui/material/TextField';

const MovieNameInput = ({ movieName, onChange, classes }) => {
  const handleTextChange = (e) => {
    e.preventDefault();
    const value = e.target.value
    onChange(value);
  };

  return (
    <TextField 
      id="outlined-basic" 
      variant="outlined"
      placeholder="Digite o nome de um filme"
      value={movieName}
      onChange={(e) => handleTextChange(e)}
      InputProps={{
        style: {
          width: '40vh',
          color: 'white',
          border: '1px solid'
        }
      }}
    />
  )
};

export default MovieNameInput;
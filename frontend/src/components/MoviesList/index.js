import React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import './styles.css'

const MoviesList = ({ movies }) => {
  const renderList = () => {
    return (
      <div className='movies-list-container'>
        {movies.map((movie, index) => (
          <ListItem key={index}>
            <ListItemText primary={movie} />
          </ListItem>
        ))}
      </div>
    )
  }

  return (
    <List style={{ overflow: 'auto' }}>
      {renderList()}
    </List>
  )
};

export default MoviesList;
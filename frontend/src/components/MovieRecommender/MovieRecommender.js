import React, { useState, useEffect } from 'react';
import MovieNameInput from '../MovieNameInput';
import api from '../../api/api';
import MoviesList from '../MoviesList';
import './styles.css'

const MovieRecommender = () => {
  const [movieName, setMovieName] = useState('');
  const [moviesList, setMoviesList] = useState([]);
  const [returnedMovieName, setReturnedMovieName] = useState('');

  useEffect(() => {
    return resetAll();
  }, []);

  const resetAll = () => {
    setMoviesList([]);
    setMovieName('');
    setReturnedMovieName('');
  }

  const onSearch = async () => {
    try {
      const response = await api.post('/recommender', null, {
        params: {
          movie: movieName,
          size: 20
        }
      });
      if (response.status === 200) {
        const { movies } = response.data;
        const returnedMovieName = movies[0];
        const moviesList = movies[1];
        setMoviesList(moviesList);
        setReturnedMovieName(returnedMovieName);
      }
    } catch(error) {
      console.log(error.message);
    }
  };

  const handleInputChange = (text) => {
    if (moviesList) {
      setMoviesList([])
    }
    setMovieName(text);
  };

  const showResults = moviesList.length > 0 && movieName.length > 0;

  return (
    <div className='container'>
      <div className='search-area'>
        <MovieNameInput value={movieName} onChange={handleInputChange} />
        <button onClick={onSearch} className='button'>
          Buscar
        </button>
      </div>
      {showResults ? movieName === returnedMovieName ? 
        <span className='searchLabel'>{`Exibindo recomendações baseadas no filme ${movieName}: `}</span> :
        <span className='searchLabel'>{`O filme ${movieName} não foi encontrado na base. Exibindo recomendações para o nome aproximado ${returnedMovieName}: `}</span> :
        null
      }
      {showResults && (
        <MoviesList movies={moviesList} />
      )}
    </div>
  )
};

export default MovieRecommender;
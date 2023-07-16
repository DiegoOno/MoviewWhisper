import './App.css';
import MovieRecommender from './components/MovieRecommender/MovieRecommender';

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>MovieWhisper</h1>
      </header>
      <MovieRecommender />
    </div>
  );
};

export default App;

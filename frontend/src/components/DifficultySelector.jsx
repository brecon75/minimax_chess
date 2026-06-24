function DifficultySelector({ difficulty, setDifficulty, disabled }) {
  const levels = ['Easy', 'Medium', 'Hard', 'Expert'];
  
  return (
    <div className="flex bg-[#2a2a2a] border border-[#444] rounded">
      {levels.map(level => (
        <button
          key={level}
          disabled={disabled}
          onClick={() => setDifficulty(level)}
          className={`px-3 py-1.5 text-sm transition-colors ${
            difficulty === level 
              ? 'bg-[#444] text-gray-200' 
              : 'text-gray-400 hover:bg-[#333]'
          } ${disabled ? 'opacity-50' : ''}`}
        >
          {level}
        </button>
      ))}
    </div>
  );
}

export default DifficultySelector;

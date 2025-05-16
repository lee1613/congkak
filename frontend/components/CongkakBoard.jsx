<div className="flex flex-col items-center p-4">
  <h1 className="text-2xl mb-4">Congkak Game</h1>
  <div className="grid grid-cols-9 gap-4">
    {/* Player 2 row */}
    <div className="col-span-1 bg-yellow-200 p-4 rounded-full">🏠</div>
    {[...Array(7)].map((_, i) => (
      <div key={`p2-${i}`} className="bg-green-200 p-4 rounded-full">4</div>
    ))}
    <div className="col-span-1 bg-yellow-200 p-4 rounded-full">🏠</div>

    {/* Player 1 row (reverse order) */}
    <div className="col-span-1"></div>
    {[...Array(7)].map((_, i) => (
      <div key={`p1-${i}`} className="bg-blue-200 p-4 rounded-full">4</div>
    )).reverse()}
    <div className="col-span-1"></div>
  </div>
</div>

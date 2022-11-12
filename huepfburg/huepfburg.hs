{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}

import Data.Array ((!))
import Data.Graph
import Data.Maybe (fromJust, isJust)
import Data.Set hiding (map)

type VertexPair = (Vertex, Vertex)
type OriginFunc = VertexPair -> VertexPair
-- Ein Iterationsschritt, bestehend aus möglichen Positionen, der Herkunftszuordnung und besuchten Knotenpaaren
type State = (Set Vertex, Set Vertex, Set VertexPair, OriginFunc)

-- Positionen, an denen ein Spieler im nächsten Schritt sein kann
nextPos :: Graph -> Set Vertex -> Set Vertex
nextPos graph = fromList . concatMap (graph !) . elems

-- Nächster Iterationsschritt
nextState :: Graph -> State -> State
nextState graph (pos1, pos2, pairs, origin) =
  let pos1n = nextPos graph pos1
      pos2n = nextPos graph pos2
      pairsn = union pairs (cartesianProduct pos1n pos2n)
      origin_new (p1, p2)
        | (p1, p2) `member` pairs = origin (p1, p2)
        | (p1, p2) `member` pairsn =
            let pred p pos = head [w | w <- elems pos, p `elem` graph ! w]
             in (pred p1 pos1, pred p2 pos2)
   in (pos1n, pos2n, pairsn, origin_new)

-- Findet den Weg zu einem Knotenpaar aus einer Herkunftsfunktion
startPath :: OriginFunc -> VertexPair -> [VertexPair]
startPath origin = takeWhile (/=(1, 2)) . iterate origin 

-- Findet Weg, so dass Spieler sich treffen
solve :: Graph -> State -> Maybe [VertexPair]
solve graph (pos1, pos2, pairs, origin)
  | isJust intersect = Just (startPath origin (fromJust intersect, fromJust intersect))
  | pairsn == pairs = Nothing
  | otherwise = solve graph (pos1n, pos2n, pairsn, origin_new)
  where
    (pos1n, pos2n, pairsn, origin_new) = nextState graph (pos1, pos2, pairs, origin)
    intersect = lookupMin (intersection pos1 pos2)

-- Interpretiert String als Tuple
parseTuple s = let [a, b] = map (read :: String -> Int) $ words s in (a, b)

initState :: State
initState = (singleton 1, singleton 2, singleton (1, 2), id)

main = do
  input <- getContents
  let inputLines = lines input
  let (n_nodes, n_edges) = parseTuple $ head inputLines
  let graph = buildG (1, n_nodes) $ map parseTuple $ tail inputLines
  let solution = solve graph initState
  if isJust solution
    then do
      putStrLn "Weg für Sasha:"
      putStrLn . unwords . reverse . map (show . fst) $ fromJust solution
      putStrLn "Weg für Mika:"
      putStrLn . unwords . reverse . map (show . snd) $ fromJust solution
    else putStrLn "Kein Weg gefunden!"
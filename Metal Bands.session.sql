-- @block
SELECT band_name AS Bands,formed AS FormationYear
FROM metal_bands
ORDER BY formed DESC

-- @block
SELECT DISTINCT band_name,origin,style FROM metal_bands
WHERE origin='Brazil' AND split != ''
ORDER BY band_name
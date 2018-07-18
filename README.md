# Tag_Paper

Name disambiguation system prototype for Kejso.com, a Chinese scientific resource search engine.

## Pipeline
1. Extract large amounts of scientific papers from local database for getting word embedding
2. Automatically construct 'Academic Discipline Tree' using multi-level clustering. 
    (1) Use AFKMC2 to fast pinpoint good intial points.
    (2) Use a strategy which combines AFKMC2 and affinity propagation to decide number of disciplines.
3. Extract keywords and match Paper on academic discipline tree. The distance between a paper (a set of words) and a discipline (a point on tree) is computed by weighted summation, weights depend on TF-IDF value of that word.
4. Extract author information (name, university name, department name, brief introduction, awards and so on) from local database.
5. Match author of same Chinese name to academic discipline tree. If both author names fall to same discipline, do the matching process again in the next level.

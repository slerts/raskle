# Raskle

## Backend data processor and REST API for NHL stats

#### MongoDB cache

 * Stores data dumps from the unofficial and unsupported NHL.com stats 
 endpoints that power game center
 
 * Collections: games, people, teams, divisions, conferences

#### MySQL db
  
  * Data from local cache will be processed and stored in an SQL db
  
  * Initial Data Tables: positions, people, conference, division, teams, games, 
  pp_stats, rosters, time_on_ice, plays, shots, missed_shots, 
  blocked_shots, goals, penalties, faceoffs, poss_changes, hits, 
  stoppages
  
  * __TODO__ Tables: rolling stats over each season
    * ie. what are the totals for each stat prior to each game?
  
#### API

  * __TODO__ Endpoints: conferences, divisions, people, games
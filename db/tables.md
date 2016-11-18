* Tables: 
    * positions - stores position specific data for each position, can include coaches and officials
        * Primary Key : position_code
        
    * people - stores specific data for each player, can include coaches and officials
        * Primary Key : pid
        * Foreign Key : position_code -> positions(position_code)
        
    * conference - stores conference specific data for each conference in the league
        * Primary Key : conference_id
        
    * division - stores division specific data for each division in each conference
        * Primary Key : division_id
        * Foreign Key : conference_id -> conferences(conference_id)
        
    * teams - stores team specific data for each team in the league
        * Primary Key : team_id
        * Foreign Key : division_id -> divisions(division_id)
        * Foreign Key : conference_id -> conferences(conference_id)
        
    * games - stores basic game data
        * Primary Key : game_id
        * Foreign Key : home_team_id -> teams(team_id)
        * Foreign Key : away_team_id -> teams(team_id)
        * Foreign Key : first_star_pid -> people(pid)
        * Foreign Key : second_star_pid -> people(pid)
        * Foreign Key : third_star_pid -> people(pid)
        
    * pp_stats - stores pp info of both teams for a game
        * Primary Key : game_id
        * Foreign Key : game_id -> games(game_id)
        
    * rosters - stores the rosters of each team for each game
        * Primary Keys : game_id, player_id
        * Foreign Key : game_id -> games(game_id)
        * Foreign Key : pid -> people(pid)
        * Foreign Key : team_id -> teams(team_id)
        
    * time_on_ice - stores the time on ice info of each player for each game
        * Primary Key : game_id, player_id
        * Foreign Key : game_id -> games(game_id)
        * Foreign Key : pid -> people(pid)
        
    * plays - stores the basic data for every play recorded
        * Primary Key : game_id, event_idx
        * Foreign Key : game_id -> games(game_id)
        
    * shots - stores shot specific data for each shot
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
        * Foreign Key : shooter_pid -> people(pid)
        * Foreign Key : goalie_pid -> people(pid)
        
    * missed_shots - stores missed shot specific data for each missed shot
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
        * Foreign Key : shooter_pid -> people(pid)
        
    * blocked_shots - stores blocked_shot specific data for each blocked_shot
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
        * Foreign Key : shooter_pid -> people(pid)
        * Foreign Key : blocker_pid -> people(pid)
        
    * goals - stores goal specific data for each goal
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
        * Foreign Key : shooter_pid -> people(pid)
        * Foreign Key : assist_1_pid -> people(pid)
        * Foreign Key : assist_2_pid -> people(pid)
        * Foreign Key : goalie_pid -> people(pid)
        
    * penalties - stores penalty specific data for each penalty
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
        * Foreign Key : penalty_on_pid -> people(pid)
        * Foreign Key : drawn_by_pid -> people(pid)
        
    * faceoffs - stores faceoff specific data for each faceoff
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
        * Foreign Key : winner_pid -> people(pid)
        * Foreign Key : loser_pid -> people(pid)
        
    * poss_changes - stores possesion change specific data for each giveaway or takeaway
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
        * Foreign Key : pid -> people(pid)
        
    * hits - stores hit specific data for each hit
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
        * Foreign Key : hitter_pid -> people(pid)
        * Foreign Key : hittee_pid -> people(pid)
        
    * stoppages - stores stoppage specific data for each time play is stopped
        * Primary Key : game_id, event_idx
        * Foreign Key : (game_id, event_idx) -> plays(game_id, event_idx)
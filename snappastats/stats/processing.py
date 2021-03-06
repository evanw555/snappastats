from .models import Game, Team, Player, Profile, DigestedStats


def generate_game(data):
    """
    :param data: Data that represents game to be generated.
    {
        date,
        teams: [
            {
                players: [
                    {
                        id, points, shots, misses, scorable, catches, sinks
                    }, {
                    ...
                    }
                ]
            }, {
                players: [
                    {
                        ...
                    }, {
                        ...
                    }
                ]
            }
        ]
    }
    :return:
    """
    game = Game()
    game.date = data['date']
    game.save()
    team_models = []
    profile_ids = []
    for ti in range(2):
        team_data = data['teams'][ti]
        team = Team()
        team.game = game
        team.save()
        player_models = []
        for pi in range(2):
            player_data = team_data['players'][pi]
            player = Player()
            player.profile = Profile.objects.get(pk=player_data['id'])
            player.points = player_data['points']
            player.shots = player_data['shots']
            player.misses = player_data['misses']
            player.scorable = player_data['scorable']
            player.catches = player_data['catches']
            player.sinks = player_data['sinks']
            player.team = team
            player.save()
            player_models.append(player)
            profile_ids.append(player_data['id'])
        # Link partners
        for i in range(2):
            player_models[i].partner = player_models[1 - i]
            player_models[i].save()
        # Save
        team.save()
        team_models.append(team)
    # Link opposing teams
    for i in range(2):
        team_models[i].opposing_team = team_models[1 - i]
        team_models[i].save()
    # Save
    game.save()
    # Return IDs of players affected
    return profile_ids


def digest(profile_id):
    profile = Profile.objects.get(pk=profile_id)
    digested_stats = profile.digested_stats
    if not digested_stats:
        digested_stats = DigestedStats()
        digested_stats.save()
        profile.digested_stats = digested_stats
        profile.save()
    stats = {
        'games': 0,
        'points': 0,
        'sinks': 0,
        'shots': 0,
        'misses': 0,
        'scorable': 0,
        'catches': 0,
        'partner_catches': 0,
        'opponent_scorable': 0,
        'teammates': {}
    }

    # Collect total measurements
    for player in profile.players.all():
        stats['games'] += 1
        stats['points'] += player.points
        stats['sinks'] += player.sinks
        stats['shots'] += player.shots
        stats['misses'] += player.misses
        stats['scorable'] += player.scorable
        stats['catches'] += player.catches
        stats['partner_catches'] += player.partner.catches
        stats['opponent_scorable'] += player.team.opposing_team.get_combined('scorable')
        partner_name = player.partner.get_fullname()
        if partner_name in stats['teammates']:
            stats['teammates'][partner_name] += 1
        else:
            stats['teammates'][partner_name] = 1
    stats['normal'] = stats['shots'] - stats['scorable'] - stats['misses']  # normal = non-scorable tables and lows

    # Assign values to stats
    digested_stats.games = stats['games']
    digested_stats.points = stats['points']
    digested_stats.sinks = stats['sinks']
    digested_stats.shots = stats['shots']
    digested_stats.misses = stats['misses']
    digested_stats.scorable = stats['scorable']
    # Most common teammates
    if len(stats['teammates']) > 0:
        max_partner = max(stats['teammates'], key=lambda k: stats['teammates'][k])
        digested_stats.common_teammates = \
            ', '.join([k for k in stats['teammates'] if stats['teammates'][k] == stats['teammates'][max_partner]])
    else:
        digested_stats.common_teammates = 'None'
    # Throwing score
    denom = stats['shots']
    numerator = (stats['points'] + stats['scorable'] + (.5 * stats['normal'])) * 100
    throwing_before_clamp = 0 if not denom else round(numerator / denom)
    digested_stats.throwing_score = throwing_before_clamp if throwing_before_clamp <= 100 else 100
    # Catching score
    denom = stats['opponent_scorable'] - stats['partner_catches']
    digested_stats.catching_score = 0 if not denom else round(stats['catches'] * 100 / denom)
    digested_stats.save()



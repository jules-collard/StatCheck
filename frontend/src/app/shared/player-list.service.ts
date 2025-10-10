import { httpResource } from "@angular/common/http";
import { SkaterLeaderboardItem } from "../leaderboard-page/skater-leaderboard-item.model";
import { PlayerListItem } from "../search-page/player-list/player-list-item.model";
import { computed, signal } from "@angular/core";
import { FilterParams } from "../search-page/player-filter/filter-params.interface";

export interface LeaderboardConfig {
    season: number;
    playerType: 'skaters' | 'goalies';
    gameType: 2 | 3;
}

export interface ListConfig {
    type: 'search' | 'leaderboard';
    leaderboardConfig: LeaderboardConfig | null;
}

export class PlayerListService<T extends PlayerListItem | SkaterLeaderboardItem> {

    private listConfig = signal<ListConfig | null>(null)

    private playerListResource = httpResource<T[]>(() => {
        if (this.listConfig()) {
            switch (this.listConfig()!.type) {
                case 'search':
                    return 'http://localhost:5000/api/players';
                case 'leaderboard':
                    if (this.listConfig()!.leaderboardConfig) {
                        return `http://localhost:5000/api/leaderboards/${this.listConfig()!.leaderboardConfig!.season}/${this.listConfig()!.leaderboardConfig!.playerType}?gameType=${this.listConfig()!.leaderboardConfig!.gameType}`;
                    }
            }
        }
        return undefined;
    })

    filteredPlayers = computed<T[]>(() => {
        if (this.listConfig() && this.playerListResource.hasValue()) {
            return this.playerListResource.value();
        } else {
            return [];
        }
    })

    filterParams = signal<FilterParams>({
        nameToSearch: '',
        team: 'All',
        active: true,
        retired: true,
        goalie: true,
        defenseman: true,
        forward: true
    })

    setConfig(config: ListConfig) {
        this.listConfig.set(config);
    }
    
}
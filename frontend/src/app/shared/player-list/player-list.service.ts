import { httpResource } from "@angular/common/http";
import { SkaterLeaderboardItem } from "../../leaderboard-page/skater-leaderboard-item.model";
import { PlayerListItem } from "../../search-page/player-list/player-list-item.model";
import { computed, signal } from "@angular/core";
import { FilterParams } from "../../search-page/player-filter/filter-params.interface";

export interface LeaderboardConfig {
    season: number;
    playerType: 'skaters' | 'goalies';
    gameType: 2 | 3;
}

export interface ListConfig {
    type: 'search' | 'leaderboard';
    itemsPerPage: number;
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

    private filteredPlayers = computed<T[]>(() => {
        if (this.listConfig() && this.playerListResource.hasValue()) {
            return this.playerListResource.value();
        } else {
            return [];
        }
    })

    slicedPlayers = computed<T[]>(() => {
        if (this.listConfig()) {
            return this.filteredPlayers().slice(this.currPage() * this.listConfig()!.itemsPerPage, (this.currPage() + 1) * this.listConfig()!.itemsPerPage)
        } else {
            return []
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

    currPage = signal<number>(0)
    maxPages = computed<number>(() => {
        if (this.listConfig()) {
            return Math.ceil(this.filteredPlayers().length / this.listConfig()!.itemsPerPage);
        } else {
            return 1;
        }
    })

    nextPage() {
        this.currPage.set(Math.min(this.currPage() + 1, this.maxPages() - 1));
    }

    prevPage() {
        this.currPage.set(Math.max(this.currPage() - 1, 0));
    }

    firstPage() {
        this.currPage.set(0);
    }

    lastPage() {
        this.currPage.set(this.maxPages() - 1);
    }
    
}
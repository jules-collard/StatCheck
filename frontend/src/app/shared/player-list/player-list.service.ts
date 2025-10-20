import { httpResource } from "@angular/common/http";
import { SkaterLeaderboardItem } from "../../skater-leaderboard-page/skater-leaderboard-item.model";
import { PlayerListItem } from "../../search-page/player-list/player-list-item.model";
import { computed, effect, inject, signal } from "@angular/core";
import { FilterParams } from "../../search-page/player-filter/filter-params.interface";
import { TableSortService } from "../table-sort.service";

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

    private sortService = inject(TableSortService);

    private listConfig = signal<ListConfig | null>(null);

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
            return this.playerListResource.value().filter((player) => {
                switch (this.listConfig()!.type) {
                    case 'search':
                        return (
                            player.fullName.toLowerCase().includes(this.filterParams().nameToSearch)
                            && (this.filterParams().active === player.isActive || this.filterParams().retired === !player.isActive)
                            && (this.positionsToShow().includes(player.position))
                            && (this.filterParams().team === 'All' ? true : this.filterParams().team === (player as PlayerListItem).teamTriCode)
                        )
                    case 'leaderboard':
                        return (
                            player.fullName.toLowerCase().includes(this.filterParams().nameToSearch)
                            && (this.filterParams().active === player.isActive || this.filterParams().retired === !player.isActive)
                            && (this.positionsToShow().includes(player.position))
                            && (this.filterParams().team === 'All' ? true : (player as SkaterLeaderboardItem).teamTriCodes.includes(this.filterParams().team))
                        )
                }
            })
        } else {
            return [];
        }
    })

    dataEffect = effect(() => {
        this.sortService.setData(this.filteredPlayers());
    })

    // Filtering
    positionsToShow = computed<string[]>(() => {
        let pos = [];
        if (this.filterParams().goalie) {pos.push('G');}
        if (this.filterParams().defenseman) {pos.push('D');}
        if (this.filterParams().forward) {pos.push('L', 'R', 'C');}
        return pos
    })

    teams = computed<string[]>(() => {
        if (this.playerListResource.hasValue() && this.listConfig()) {
            switch (this.listConfig()!.type) {
                case 'search':
                    return [... new Set(this.playerListResource.value()
                    .map((player) => (player as PlayerListItem).teamTriCode)
                    .filter((triCode) => triCode !== null)
                    .sort())];
                case 'leaderboard':
                    return [... new Set(this.playerListResource.value()
                    .map((player) => (player as SkaterLeaderboardItem).teamTriCodes)
                    .flat()
                    .sort())];
            }
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

    slicedPlayers = computed<T[]>(() => {
        if (this.listConfig()) {
            return this.sortService.sortedData().slice(this.currPage() * this.listConfig()!.itemsPerPage, (this.currPage() + 1) * this.listConfig()!.itemsPerPage)
        } else {
            return []
        }
    })

    setConfig(config: ListConfig) {
        this.listConfig.set(config);
    }

    // Paging logic
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
import { httpResource } from "@angular/common/http";
import { computed, Injectable, signal } from "@angular/core";
import { PlayerListItem } from "./player-list-item.model";
import { FilterParams } from "../player-filter/filter-params.interface";

@Injectable({
    providedIn: 'root'
})
export class PlayerListService {
    private URL = 'http://localhost:5000/api/players'

    private shouldFetch = signal<boolean>(false)
    filterParams = signal<FilterParams>({
        nameToSearch: '',
        team: 'All',
        active: true,
        retired: true,
        goalie: true,
        defenseman: true,
        forward: true
    })
    
    allPlayers = httpResource<PlayerListItem[]>(() => {
        const shouldFetch = this.shouldFetch();
        return shouldFetch ? this.URL : undefined;
    });

    positionsToShow = computed<string[]>(() => {
        let pos = [];
        if (this.filterParams().goalie) {pos.push('G');}
        if (this.filterParams().defenseman) {pos.push('D');}
        if (this.filterParams().forward) {pos.push('L', 'R', 'C');}
        return pos
    })

    filteredPlayers = computed<PlayerListItem[]>(() => {
        if (this.allPlayers.hasValue()) {
            return this.allPlayers.value().filter((player) => {
                return (
                    player.fullName.toLowerCase().includes(this.filterParams().nameToSearch)
                    && (this.filterParams().active === player.isActive || this.filterParams().retired === !player.isActive)
                    && (this.positionsToShow().includes(player.position))
                    && (this.filterParams().team === 'All' ? true : this.filterParams().team === player.teamTriCode)
                )
            })
        } else { return [] }
    })

    teams = computed<string[]>(() => {
        if (this.allPlayers.hasValue()) {
            return [... new Set(this.allPlayers.value()
                .map((player) => player.teamTriCode)
                .filter((triCode) => triCode !== null)
                .sort())]
        } else { return [] }
    })

    setNameToSearch(name: string) {
        this.filterParams.update(params => ({...params, nameToSearch: name}));
    }

    reset() {
        this.filterParams.set({
            nameToSearch: '',
            team: 'All',
            active: true,
            retired: true,
            goalie: true,
            defenseman: true,
            forward: true
        });
    }

    fetch() {
        this.shouldFetch.set(true)
    }
}
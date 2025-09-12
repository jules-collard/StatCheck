import { HttpParams, httpResource } from "@angular/common/http";
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
        hideRetired: false
    })
    
    allPlayers = httpResource<PlayerListItem[]>(() => {
        const shouldFetch = this.shouldFetch();
        return shouldFetch ? this.URL : undefined;
    });

    filteredPlayers = computed<PlayerListItem[]>(() => {
        if (this.allPlayers.hasValue()) {
            return this.allPlayers.value().filter((player) => {
                return (
                    player.fullName.toLowerCase().includes(this.filterParams().nameToSearch)
                    && this.filterParams().hideRetired ? player.isActive === true : true
                )
            })
        } else { return [] }
    })

    setNameToSearch(name: string) {
        this.filterParams.update(params => ({...params, nameToSearch: name}));
    }

    setHideRetired(val: boolean) {
        this.filterParams.update(params => ({...params, hideRetired: val}));
    }

    reset() {
        this.filterParams.update(params => ({...params, nameToSearch: ''}));
    }

    fetch() {
        this.shouldFetch.set(true)
    }
}
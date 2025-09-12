import { httpResource } from "@angular/common/http";
import { computed, Injectable, signal } from "@angular/core";
import { PlayerListItem } from "./player-list-item.model";

@Injectable({
    providedIn: 'root'
})
export class PlayerListService {
    private URL = 'http://localhost:5000/api/players'

    private shouldFetch = signal<boolean>(false)
    nameToSearch = signal<string>('')
    
    allPlayers = httpResource<PlayerListItem[]>(() => {
        const shouldFetch = this.shouldFetch();
        return shouldFetch ? this.URL : undefined;
    });

    filteredPlayers = computed<PlayerListItem[]>(() => {
        if (this.allPlayers.hasValue()) {
            return this.allPlayers.value().filter((player) => {
                return player?.fullName.toLowerCase().includes(this.nameToSearch()!)
            })
        } else { return [] }
    })

    setNameToSearch(name: string) {
        this.nameToSearch.set(name)
    }

    reset() {
        this.nameToSearch.set('')
    }

    fetch() {
        this.shouldFetch.set(true)
    }
}
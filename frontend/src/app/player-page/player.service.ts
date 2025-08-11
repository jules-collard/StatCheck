import { inject, Injectable } from "@angular/core";
import { Player } from "./player.model";
import { HttpClient } from "@angular/common/http";
import { SearchResult } from "../search/search-result.model";
import { SeasonTotals } from "./player-season-totals/season-totals.model";

@Injectable({
    providedIn: 'root'
})
export class PlayerService {
    private httpClient = inject(HttpClient)

    fetchPlayerData(id: number) {
        return this.httpClient.get<Player>(`http://localhost:5000/api/players/${id}`)
    }

    fetchSeasonTotals(id: number) {
        return this.httpClient.get<SeasonTotals[]>(`http://localhost:5000/api/players/${id}/stats`)
    }

    fetchAllPlayers() {
        return this.httpClient.get<SearchResult[]>('http://localhost:5000/api/players')
    }
}
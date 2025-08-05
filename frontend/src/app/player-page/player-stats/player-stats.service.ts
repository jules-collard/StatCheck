import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { SeasonStats } from "./season-stats.model";

@Injectable({
    providedIn: 'root'
})
export class PlayerStatsService {
    private httpClient = inject(HttpClient)

    fetchPlayerStats(id: number) {
        return this.httpClient.get<SeasonStats[]>(`http://localhost:5000/api/players/${id}/stats`)
    }
}
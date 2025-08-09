import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { SeasonTotals } from "./season-totals.model";

@Injectable({
    providedIn: 'root'
})
export class PlayerSeasonTotalsService {
    private httpClient = inject(HttpClient)

    fetchSeasonTotals(id: number) {
        return this.httpClient.get<SeasonTotals[]>(`http://localhost:5000/api/players/${id}/stats`)
    }
}
import { inject, Injectable } from "@angular/core";
import { Player } from "./player.model";
import { HttpClient } from "@angular/common/http";

@Injectable({
    providedIn: 'root'
})
export class PlayerService {
    private httpClient = inject(HttpClient)

    fetchPlayerData(id: number) {
        return this.httpClient.get<Player>(`http://localhost:5000/api/players/${id}`)
    }
}
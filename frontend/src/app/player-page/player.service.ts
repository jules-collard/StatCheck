import { Injectable, signal } from "@angular/core";
import { Player } from "./player.model";
import { httpResource } from "@angular/common/http";
import { SeasonTotals } from "./player-season-totals/season-totals.model";

@Injectable({
    providedIn: 'root'
})
export class PlayerService {

    private playerID = signal<number | null>(null);

    private playerData = httpResource<Player>(() => `http://localhost:5000/api/players/${this.playerID()}`);
    private seasonTotals = httpResource<SeasonTotals[]>(() => `http://localhost:5000/api/players/${this.playerID()}/stats`);
    
    getPlayerData() {
        if (this.playerData.hasValue()) {
            return this.playerData.value();
        } else return null;
    }

    playerDataIsLoading() {
        return this.playerData.isLoading();
    }

    getSeasonTotals() {
        if (this.seasonTotals.hasValue()) {
            return this.seasonTotals.value();
        } else return null;
    }

    seasonTotalsIsLoading() {
        return this.seasonTotals.isLoading();
    }

    setPlayerID(id: number) {
        this.playerID.set(id)
        console.log('ID Set to' + this.playerID())
    }
}
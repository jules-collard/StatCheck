import { Injectable, signal } from "@angular/core";
import { Player } from "./player.model";
import { httpResource } from "@angular/common/http";
import { SeasonTotals } from "./season-totals-table/season-totals.model";
import { GoalieTotals } from "./goalie-totals-table/goalie-totals.model";

@Injectable({
    providedIn: 'root'
})
export class PlayerService {

    private playerID = signal<number | null>(null);

    private playerData = httpResource<Player>(() => `http://localhost:5000/api/players/${this.playerID()}`);
    private regSeasonTotals = httpResource<SeasonTotals[] | GoalieTotals[]>(() => `http://localhost:5000/api/players/${this.playerID()}/stats?gameType=2`);
    private postSeasonTotals = httpResource<SeasonTotals[] | GoalieTotals[]>(() => `http://localhost:5000/api/players/${this.playerID()}/stats?gameType=3`)
    
    getPlayerData() {
        if (this.playerData.hasValue()) {
            return this.playerData.value();
        } else return null;
    }

    playerDataIsLoading() {
        return this.playerData.isLoading();
    }

    getRegSeasonTotals(): SeasonTotals[] | GoalieTotals[] | null {
        if (this.regSeasonTotals.hasValue()) {
            return this.regSeasonTotals.value();
        } else return null;
    }

    getPostSeasonTotals(): SeasonTotals[] | GoalieTotals[] | null {
        if (this.postSeasonTotals.hasValue()) {
            return this.postSeasonTotals.value();
        } else return null;
    }

    seasonTotalsIsLoading() {
        return this.regSeasonTotals.isLoading() || this.postSeasonTotals.isLoading();
    }

    setPlayerID(id: number) {
        this.playerID.set(id)
        console.log('ID Set to' + this.playerID())
    }
}
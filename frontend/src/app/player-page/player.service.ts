import { computed, Injectable, signal } from "@angular/core";
import { Player } from "./player.model";
import { httpResource } from "@angular/common/http";
import { SkaterStats } from "./skater-stats.model";
import { GoalieStats } from "./goalie-stats.model";
import { SkaterSeasonRecords } from "./season-totals-table/skater-season-records.model";
import { GoalieSeasonRecords } from "./goalie-totals-table/goalie-season-records.model";

@Injectable({
    providedIn: 'root'
})
export class PlayerService {

    private playerID = signal<number | null>(null);

    private playerData = httpResource<Player>(() => `http://localhost:5000/api/players/${this.playerID()}`);
    private regSeasonStats = httpResource<SkaterStats[] | GoalieStats[]>(() => `http://localhost:5000/api/players/${this.playerID()}/stats?gameType=2`);
    private postSeasonStats = httpResource<SkaterStats[] | GoalieStats[]>(() => `http://localhost:5000/api/players/${this.playerID()}/stats?gameType=3`);

    getPlayerData() {
        if (this.playerData.hasValue()) {
            return this.playerData.value();
        } else return null;
    }

    playerDataIsLoading() {
        return this.playerData.isLoading();
    }

    getRegSeasonStats(): SkaterStats[] | GoalieStats[] | null {
        if (this.regSeasonStats.hasValue()) {
            return this.regSeasonStats.value();
        } else return null;
    }

    getPostSeasonStats(): SkaterStats[] | GoalieStats[] | null {
        if (this.postSeasonStats.hasValue()) {
            return this.postSeasonStats.value();
        } else return null;
    }

    seasonStatsIsLoading(): boolean {
        return this.regSeasonStats.isLoading() || this.regSeasonStats.isLoading();
    }

    setPlayerID(id: number) {
        this.playerID.set(id)
        console.log('ID Set to' + this.playerID())
    }
}
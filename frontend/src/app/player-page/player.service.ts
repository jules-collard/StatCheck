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
    private skaterRegSeasonRecords = httpResource<SkaterSeasonRecords[]>(() => `http://localhost:5000/api/records/skaters/2`)
    private goalieRegSeasonRecords = httpResource<GoalieSeasonRecords[]>(() => 'http://localhost:5000/api/records/goalies/2')

    getPlayerData() {
        if (this.playerData.hasValue()) {
            return this.playerData.value();
        } else return null;
    }

    playerDataIsLoading() {
        return this.playerData.isLoading();
    }

    getRegSeasonTotals(): SkaterStats[] | GoalieStats[] | null {
        if (this.regSeasonStats.hasValue()) {
            return this.regSeasonStats.value();
        } else return null;
    }

    getPostSeasonTotals(): SkaterStats[] | GoalieStats[] | null {
        if (this.postSeasonStats.hasValue()) {
            return this.postSeasonStats.value();
        } else return null;
    }

    seasonTotalsIsLoading(): boolean {
        return this.regSeasonStats.isLoading() || this.regSeasonStats.isLoading();
    }

    getSkaterRecords(): SkaterSeasonRecords[] | null {
        if (this.skaterRegSeasonRecords.hasValue()) {
            return this.skaterRegSeasonRecords.value();
        } else return [];
    }

    getGoalieRecords(): GoalieSeasonRecords[] | null {
        if (this.goalieRegSeasonRecords.hasValue()) {
            return this.goalieRegSeasonRecords.value();
        } else return [];
    }

    setPlayerID(id: number) {
        this.playerID.set(id)
        console.log('ID Set to' + this.playerID())
    }
}
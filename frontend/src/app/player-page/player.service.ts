import { Injectable, signal } from "@angular/core";
import { Player } from "./player.model";
import { httpResource } from "@angular/common/http";
import { SkaterStats } from "./skater-stats.model";
import { GoalieStats } from "./goalie-stats.model";

@Injectable({
    providedIn: 'root'
})
export class PlayerService {

    private PLAYER_URL = 'http://localhost:5000/api/players'

    private shouldFetch = signal<boolean>(false)
    private playerID = signal<number | null>(null);

    playerData = httpResource<Player>(() => {
        const shouldFetch = this.shouldFetch();
        return shouldFetch ? `${this.PLAYER_URL}/${this.playerID()}` : undefined;
    });
    regSeasonStats = httpResource<SkaterStats[] | GoalieStats[]>(() => {
        const shouldFetch = this.shouldFetch();
        return shouldFetch ? `${this.PLAYER_URL}/${this.playerID()}/stats?gameType=2` : undefined
    }, {
        'defaultValue': []
    });
    postSeasonStats = httpResource<SkaterStats[] | GoalieStats[]>(() => {
        const shouldFetch = this.shouldFetch();
        return shouldFetch ? `${this.PLAYER_URL}/${this.playerID()}/stats?gameType=3` : undefined
    }, {
        'defaultValue': []
    });

    setPlayerID(id: number) {
        this.playerID.set(id)
        console.log('ID Set to' + this.playerID())
    }

    fetch() {
        this.shouldFetch.set(true)
    }
}
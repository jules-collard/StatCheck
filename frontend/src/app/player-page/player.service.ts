import { inject, Injectable, signal } from "@angular/core";
import { Player } from "./player.model";
import { httpResource } from "@angular/common/http";
import { SkaterStats } from "./skater-stats.model";
import { GoalieStats } from "./goalie-stats.model";
import { GlobalConfigService } from "../shared/global-config.service";

@Injectable()
export class PlayerService {
    configService = inject(GlobalConfigService)

    private PLAYER_URL = `${this.configService.backendURL}/players`
    private playerID = signal<number | null>(null);

    playerData = httpResource<Player>(() => {
        if (this.playerID()) {
            return `${this.PLAYER_URL}/${this.playerID()}`;
        } else {
            return undefined;
        }
    });
    regSeasonStats = httpResource<SkaterStats[] | GoalieStats[]>(() => {
        if (this.playerID()) {
            return `${this.PLAYER_URL}/${this.playerID()}/stats?gameType=2`;
        } else {
            return undefined;
        }
    });
    postSeasonStats = httpResource<SkaterStats[] | GoalieStats[]>(() => {
        if (this.playerID()) {
            return `${this.PLAYER_URL}/${this.playerID()}/stats?gameType=3`;
        } else {
            return undefined;
        }
    });

    setPlayerID(id: number) {
        this.playerID.set(id)
    }
}
import { httpResource } from "@angular/common/http";
import { Injectable, signal } from "@angular/core";
import { SkaterLeaderboardItem } from "./skater-leaderboard-item.model";

export interface LeaderboardConfig {
    season: number;
    playerType: 'skaters' | 'goalies';
    gameType: 2 | 3;
}

@Injectable()
export class LeaderboardService {
    private config = signal<LeaderboardConfig | null>(null);

    leaderboard = httpResource<SkaterLeaderboardItem[]>(() => {
        if (this.config()) {
            return `http://localhost:5000/api/leaderboards/${this.config()!.season}/${this.config()!.playerType}?gameType=${this.config()!.gameType}`;
        } else {
            return undefined;
        }
    })

    setConfig(config: LeaderboardConfig) {
        this.config.set(config);
    }

    getLeaderboard(): SkaterLeaderboardItem[] {
        if (this.leaderboard.hasValue()) {
            return this.leaderboard.value()
        } else {
            return []
        }
    }
}
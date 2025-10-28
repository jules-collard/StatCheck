import { Routes } from "@angular/router";
import { PlayerPage } from "./player-page/player-page";
import { SearchPage } from "./search-page/search-page";
import { HomePage } from "./home-page/home-page";
import { SkaterLeaderboardPage } from "./skater-leaderboard-page/skater-leaderboard-page";
import { GoalieLeaderboardPage } from "./goalie-leaderboard-page/goalie-leaderboard-page";

export const routes: Routes = [
    {
        path: '',
        component: HomePage
    },
    {
        path: 'players/:playerID',
        component: PlayerPage
    },
    {
        path: 'leaderboards/:season/skaters',
        component: SkaterLeaderboardPage
    },
    {
        path: 'leaderboards/:season/goalies',
        component: GoalieLeaderboardPage
    },
    {
        path: 'search',
        component: SearchPage
    }
]
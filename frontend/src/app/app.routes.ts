import { Routes } from "@angular/router";
import { PlayerPage } from "./player-page/player-page";

export const routes: Routes = [
    {
        path: 'players/:playerID',
        component: PlayerPage
    }
]
import { Injectable } from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class GlobalConfigService {
    backendURL: string = 'http://localhost:80/api'
    currentSeason: number = 20252026
    seasons: number[] = [20102011, 20112012, 20122013, 20132014, 20142015, 20152016, 20162017, 20172018, 20182019, 20192020, 20202021, 20212022, 20222023, 20232024, 20242025, 20252026]
}
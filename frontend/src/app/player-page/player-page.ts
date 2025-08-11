import { Component, inject, input, OnInit } from '@angular/core';

import { PlayerDetails } from "./player-details/player-details";
import { PlayerSeasonTotals } from "./player-season-totals/player-season-totals";
import { PlayerService } from './player.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-player-page',
  imports: [PlayerDetails, PlayerSeasonTotals],
  templateUrl: './player-page.html',
  styleUrl: './player-page.css'
})
export class PlayerPage implements OnInit {
  private playerService = inject(PlayerService);
  private activatedRoute = inject(ActivatedRoute);

  ngOnInit(): void {
    this.activatedRoute.paramMap.subscribe({
      next: (paramMap) => {
        this.playerService.setPlayerID(Number(paramMap.get('playerID')))
      }
    })
  }
}

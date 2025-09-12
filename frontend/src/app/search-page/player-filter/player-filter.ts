import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { PlayerListService } from '../player-list/player-list.service';

@Component({
  selector: 'app-player-filter',
  imports: [FormsModule],
  templateUrl: './player-filter.html',
  styleUrl: './player-filter.css'
})
export class PlayerFilter {
  playerListService = inject(PlayerListService)

  hideRetired: boolean = false

  onShowRetired() {
    this.playerListService.setHideRetired(this.hideRetired)
  }
}

import { Component, inject, computed } from '@angular/core';
import { PlayerService } from '../player.service';
import { AgePipe } from '../../pipes/age.pipe';
import { HeightPipe } from '../../pipes/height.pipe';
import { PositionPipe } from '../../pipes/position.pipe';

@Component({
  selector: 'app-player-details',
  imports: [AgePipe, HeightPipe, PositionPipe],
  templateUrl: './player-details.html',
  styleUrl: './player-details.css'
})
export class PlayerDetails {
  private playerService = inject(PlayerService)
  
  playerData = computed(() => {
    return this.playerService.getPlayerData()
  })
  loading = computed(() => {
    return this.playerService.playerDataIsLoading()
  })
}

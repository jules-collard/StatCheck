import { Component, computed, input } from '@angular/core';
import { Player } from '../player.model';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-player-info',
  imports: [MatCardModule],
  templateUrl: './player-info.html',
  styleUrl: './player-info.css'
})
export class PlayerInfo {
  playerData = input.required<Player>()
  playerAge = computed(() => {
    const today = new Date();
    const birthDate = new Date(this.playerData().birthDate);
    var age = today.getFullYear() - birthDate.getFullYear();
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) { age--; }
    return age;
  })
}

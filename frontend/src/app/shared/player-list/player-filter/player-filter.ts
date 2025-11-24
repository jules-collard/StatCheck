import { Component, computed, effect, inject, input, linkedSignal, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Field, form } from '@angular/forms/signals';
import { PlayerListService } from '../player-list.service';

@Component({
  selector: 'app-player-filter',
  imports: [FormsModule],
  templateUrl: './player-filter.html',
  styleUrl: './player-filter.css'
})
export class PlayerFilter {
  playerListService = inject(PlayerListService);

  searchParam = input<string>('');
  
  positionOptions = input<{goalie: boolean, defenseman: boolean, forward: boolean}>({
    goalie: true,
    defenseman: true,
    forward: true
  })
  anyPositions = computed<boolean>(() => {
    return this.positionOptions().goalie || this.positionOptions().defenseman || this.positionOptions().forward;
  })

  team = 'All';
  qualified = signal<boolean>(true);
  nameToSearch = linkedSignal<string>(() => this.searchParam());

  qualifiedEffect = effect(() => {
    this.playerListService.filterParams.update(params =>
      ({...params, qualified: this.qualified()})
    );
    this.playerListService.resetSorting();
  })

  searchEffect = effect(() => {
    this.playerListService.filterParams.update(params =>
      ({...params, nameToSearch: this.nameToSearch()})
    )
  })

  activeRetired = signal<'active' | 'retired' | null>(null);

  activeRetiredEffect = effect(() => {
    switch (this.activeRetired()) {
      case 'active': this.playerListService.filterParams.update(params => ({
        ...params, active: true, retired: false
      })); break;
      case 'retired': this.playerListService.filterParams.update(params => ({
        ...params, active: false, retired: true
      })); break;
      default: this.playerListService.filterParams.update(params => ({
        ...params, active: true, retired: true
      })); break;
    }
  })

  position = signal<'G' | 'D' | 'F' | null>(null);

  positionEffect = effect(() => {
    switch (this.position()) {
      case 'G': this.playerListService.filterParams.update(params => ({
        ...params, goalie: true, defenseman: false, forward: false
      })); break;
      case 'D': this.playerListService.filterParams.update(params => ({
        ...params, goalie: false, defenseman: true, forward: false
      })); break;
      case 'F': this.playerListService.filterParams.update(params => ({
        ...params, goalie: false, defenseman: false, forward: true
      })); break;
      default: this.playerListService.filterParams.update(params => ({
        ...params, goalie: true, defenseman: true, forward: true
      }));
    }
  })

  onTeamChange() {
    this.playerListService.filterParams.update(params => ({...params, team: this.team}))
  }
}

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerListButton } from './player-list-button';

describe('PlayerListButton', () => {
  let component: PlayerListButton;
  let fixture: ComponentFixture<PlayerListButton>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerListButton]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerListButton);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

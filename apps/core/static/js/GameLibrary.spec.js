describe('Game Library', function() {
  var GameFactory;

  beforeEach(angular.mock.module('TranscriptionGameApp'));

  beforeEach(inject(function(_GameFactory_) {
    GameFactory = _GameFactory_;
  }));

  it('should exist', function() {
    expect(GameFactory).toBeDefined();
  });

  describe('.diff', function() {
    it('should exist', function() {
      expect(GameFactory.diff).toBeDefined();
    });
  });
});

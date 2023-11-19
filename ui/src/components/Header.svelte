<script>
    import TopAppBar, { Row, Section, Title } from '@smui/top-app-bar';
</script>

<TopAppBar class="appbar" variant="standard">
    <Row>
      <Section>
        <Title class="title">Music Organizer</Title>
      </Section>
    </Row>
</TopAppBar>

<style>
    /* Hide everything above this component. */
    :global(#smui-app),
    :global(body),
    :global(html) {
      display: block !important;
      height: auto !important;
      width: auto !important;
      position: static !important;
    }

    :global(.appbar) {
        background-color: green;
        color: white;
        font-size: 18pt;
        height: 65px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }

    :global(.title) {
        padding: 20px;
    }
</style>